import os
import yaml
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from crewai import Crew, Agent, Task, Process, LLM
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
from dotenv import load_dotenv
from .tools.file_processor import FileProcessor
from .tools.website_audit import WebsiteAuditTool


load_dotenv()


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pitch_deck_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('PitchDeckCrew')

class PitchDeckCrew:
    def __init__(self):
        """Initialize the PitchDeckCrew with configuration and tools."""
        logger.info("Initializing PitchDeckCrew")
        self.config_dir = Path(__file__).parent / "config"
        self.start_time = None
        self.end_time = None
        
        # Load configs with error handling
        try:
            self.agents_config = self._load_config("agents.yaml")
            self.tasks_config = self._load_config("tasks.yaml")
            logger.info("✅ Configuration files loaded successfully")
        except FileNotFoundError as e:
            logger.warning(f"Configuration files not found: {e}")
            logger.info("Using default configuration")
            self.agents_config = self._get_default_agents_config()
            self.tasks_config = self._get_default_tasks_config()
        
        # Initialize LLM using CrewAI's native LLM class
        self.llm = self._initialize_llm()
        
        # Initialize tools
        self.tools = self._initialize_tools()
        logger.info("✅ Tools initialized successfully")

    def _initialize_llm(self):
        """Initialize LLM using CrewAI's native LLM class with proper provider syntax"""
        logger.info("Initializing LLM")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("OPENAI_API_KEY environment variable is required")
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Set the API key in environment for OpenAI
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # Use CrewAI's LLM class with OpenAI
        try:
            logger.info("Attempting to initialize OpenAI model")
            llm = LLM(
                model="gpt-4-turbo-preview",  # or "gpt-3.5-turbo" for a cheaper option
                temperature=0.1,
                max_tokens=2000,
                timeout=120
            )
            
            logger.info("✅ LLM initialized successfully with OpenAI")
            return llm
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI: {e}")
            raise Exception("Failed to initialize OpenAI LLM")

    def _load_config(self, filename: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        logger.debug(f"Loading configuration from {filename}")
        config_path = self.config_dir / filename
        if not config_path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            logger.debug(f"Successfully loaded {filename}")
            return config

    def _get_default_agents_config(self) -> Dict[str, Any]:
        """Get default agent configuration if YAML file is not found."""
        return {
            "structure_analyst": {
                "role": "Senior Business Analyst specializing in startup pitch deck analysis",
                "goal": "Extract and analyze key information from pitch decks to provide comprehensive business structure insights",
                "backstory": "You are an experienced business analyst with 10+ years of experience in evaluating startup pitch decks. You have a keen eye for identifying business model strengths, market opportunities, and potential red flags.",
                "verbose": True,
                "allow_delegation": False,
                "tools": ["document_processor", "search_tool"]
            }
        }

    def _get_default_tasks_config(self) -> Dict[str, Any]:
        """Get default task configuration if YAML file is not found."""
        return {
            "document_analysis_task": {
                "description": "Analyze the uploaded pitch deck document and extract detailed information. Focus on problem statement, solution, business model, market size, team, financials, and traction.",
                "expected_output": "A comprehensive analysis report with executive summary, problem analysis, solution overview, business model breakdown, market analysis, team assessment, financial summary, and scoring.",
                "agent": "structure_analyst"
            }
        }

    def _initialize_tools(self) -> Dict[str, BaseTool]:
        """Initialize all required tools."""
        logger.info("Initializing tools")
        tools = {}
        
        if os.getenv("SERPER_API_KEY"):
            logger.debug("Initializing search tools")
            tools["search_tool"] = SerperDevTool()
            tools["web_search_tool"] = WebsiteSearchTool()
        else:
            logger.warning("SERPER_API_KEY not found, search tools not initialized")
        
       
        try:
            logger.debug("Initializing custom tools")
            tools["website_audit_tool"] = WebsiteAuditTool()
            tools["document_processor"] = FileProcessor()
        except Exception as e:
            logger.error(f"Error initializing custom tools: {e}")
            raise
        
        logger.info(f"Initialized {len(tools)} tools")
        return tools

    def _create_agents(self) -> Dict[str, Agent]:
        """Create agents based on configuration."""
        logger.info("Creating agents")
        agents = {}
        
        for agent_id, config in self.agents_config.items():
            logger.debug(f"Creating agent: {agent_id}")
            agent_tool_names = config.get('tools', [])
            agent_tools = []
            
            for tool_name in agent_tool_names:
                if tool_name in self.tools:
                    agent_tools.append(self.tools[tool_name])
                else:
                    logger.warning(f"Tool '{tool_name}' not found for agent '{agent_id}'")
            
            
            try:
                agent = Agent(
                    role=config['role'],
                    goal=config['goal'],
                    backstory=config['backstory'],
                    verbose=bool(config.get('verbose', True)),
                    allow_delegation=bool(config.get('allow_delegation', False)),
                    tools=agent_tools,
                    llm=self.llm
                )
                agents[agent_id] = agent
                logger.debug(f"Successfully created agent: {agent_id}")
            except Exception as e:
                logger.error(f"Error creating agent {agent_id}: {e}")
                raise
        
        logger.info(f"Created {len(agents)} agents")
        return agents

    def _create_tasks(self, agents: Dict[str, Agent], context: Dict[str, Any]) -> List[Task]:
        """Create tasks based on configuration and context."""
        logger.info("Creating tasks")
        tasks = []
        task_outputs = {}  # To store task outputs for context
        
        for task_id, config in self.tasks_config.items():
            logger.debug(f"Creating task: {task_id}")
            agent_name = config['agent']
            
            if agent_name not in agents:
                logger.warning(f"Agent '{agent_name}' not found for task '{task_id}'")
                continue
            
            # Build task context from previous task outputs
            task_context = []
            if 'context' in config and config['context']:
                for context_task_id in config['context']:
                    if context_task_id in task_outputs:
                        task_context.append(task_outputs[context_task_id])
            
            # Create the task
            try:
                task = Task(
                    description=f"{config['description']}\n\nContext: {context}",
                    expected_output=config['expected_output'],
                    agent=agents[agent_name],
                    context=task_context if task_context else None
                )
                
                tasks.append(task)
                task_outputs[task_id] = task
                logger.debug(f"Successfully created task: {task_id}")
            except Exception as e:
                logger.error(f"Error creating task {task_id}: {e}")
                raise
        
        logger.info(f"Created {len(tasks)} tasks")
        return tasks

    def analyze_pitch_deck(
        self,
        pitch_deck_path: str,
        company_name: str,
        website_url: Optional[str] = None,
        analysis_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """Analyze a pitch deck and generate a comprehensive report."""
        self.start_time = time.time()
        timestamp = self._get_timestamp()
        
        try:
            if not os.path.exists(pitch_deck_path):
                raise FileNotFoundError(f"Pitch deck file not found: {pitch_deck_path}")
            
            if not company_name.strip():
                raise ValueError("Company name is required")
            
            
            supported_formats = ['.pdf', '.pptx', '.docx']
            file_ext = os.path.splitext(pitch_deck_path)[1].lower()
            if file_ext not in supported_formats:
                raise ValueError(f"Unsupported file format: {file_ext}. Supported formats: {', '.join(supported_formats)}")
            
            logger.info(f"🚀 Starting analysis for {company_name}...")
            
            
            logger.info("📄 Processing document...")
            file_processor = self.tools["document_processor"]
            processed_content = file_processor._run(pitch_deck_path)
            
           
            analysis_context = {
                'company_name': company_name,
                'analysis_type': analysis_type,
                'timestamp': timestamp,
                'file_path': pitch_deck_path,
                'document_content': str(processed_content)
            }
            
            if website_url:
                analysis_context['website_url'] = website_url
            
            logger.info("👥 Creating agents...")
            
            agents = self._create_agents()
            logger.info(f"✅ Created {len(agents)} agents")
            
            logger.info("📋 Creating tasks...")
            tasks = self._create_tasks(agents, analysis_context)
            logger.info(f"✅ Created {len(tasks)} tasks")
            
            if not tasks:
                raise ValueError("No tasks were created. Check your configuration.")
            
            
            logger.info("🚀 Starting crew execution...")
            crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                verbose=True,
                process=Process.sequential
            )
            
           
            result = crew.kickoff()
            logger.info("✅ Crew execution completed")
            
            if hasattr(result, 'raw'):
                content = result.raw
            elif hasattr(result, 'output'):
                content = result.output
            else:
                content = str(result)
            
           
            report_path = self._save_report(content, timestamp, company_name)
            
            self.end_time = time.time()
            duration = self._get_analysis_duration()
            
            logger.info(f"✅ Analysis completed in {duration:.2f} seconds")
            
            return {
                "status": "success",
                "report_path": str(report_path),
                "timestamp": timestamp,
                "content": content,
                "company_name": company_name,
                "analysis_type": analysis_type,
                "duration_seconds": duration,
                "file_analyzed": pitch_deck_path,
                "website_url": website_url
            }
            
        except Exception as e:
            self.end_time = time.time()
            duration = self._get_analysis_duration()
            
            error_msg = f"Analysis failed: {str(e)}"
            logger.error(f"❌ {error_msg}")
            
            return {
                "status": "error",
                "message": error_msg,
                "error_type": type(e).__name__,
                "timestamp": timestamp,
                "duration_seconds": duration,
                "file_analyzed": pitch_deck_path,
                "website_url": website_url,
                "company_name": company_name
            }

    def _get_timestamp(self) -> str:
        """Generate a timestamp string."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            logger.debug(f"Generated timestamp: {timestamp}")
            return timestamp
        except Exception as e:
            logger.error(f"Error generating timestamp: {e}")
            fallback = str(int(time.time()))
            logger.debug(f"Using fallback timestamp: {fallback}")
            return fallback

    def _get_analysis_duration(self) -> float:
        """Calculate analysis duration."""
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            logger.debug(f"Analysis duration: {duration:.2f} seconds")
            return duration
        logger.warning("Start or end time not set, duration calculation failed")
        return 0.0

    def _save_report(self, result: str, timestamp: str, company_name: str) -> str:
        """Save the analysis report to a file."""
        logger.info(f"Saving report for {company_name}")
        try:
            
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            
            clean_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            clean_name = clean_name.replace(' ', '_')
            
           
            filename = f"{clean_name}_analysis_{timestamp}.txt"
            file_path = reports_dir / filename
            
           
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Investment Analysis Report\n")
                f.write(f"## Company: {company_name}\n")
                f.write(f"## Generated: {timestamp}\n\n")
                f.write(str(result))
            
            logger.info(f"📄 Report saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"❌ Error saving report: {e}")
            fallback_path = f"analysis_{timestamp}.txt"
            try:
                with open(fallback_path, 'w', encoding='utf-8') as f:
                    f.write(str(result))
                logger.info(f"Saved report to fallback location: {fallback_path}")
                return fallback_path
            except Exception as e2:
                logger.error(f"❌ Fallback save also failed: {e2}")
                return "report_save_failed.txt"