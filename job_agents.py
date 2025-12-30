import os
import logging
import asyncio
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)
from agents.mcp import MCPServer
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

async def run_analysis(mcp_server: MCPServer, linkedin_url: str, api_key: str):
    logger.info(f"Starting analysis for LinkedIn URL: {linkedin_url}")
    # api_key = os.environ["GEMINI_API_KEY"]
    base_url = "https://generativelanguage.googleapis.com/v1beta/" 
    client = AsyncOpenAI(base_url=base_url, api_key=api_key)
    model_name = "gemini-2.5-flash"
    set_tracing_disabled(disabled=True)
    
    linkedin_agent = Agent(
            name="LinkedIn Profile Analyzer",
            instructions=f"""You are a LinkedIn profile analyzer.
            Analyze profiles for:

            - Professional experience and career progression
            - Education and certifications
            - Core skills and expertise
            - Current role and company
            - Previous roles and achievements
            - Industry reputation (recommendations/endorsements)

            Provide a structured analysis with bullet points and a brief executive summary.
            """,
            mcp_servers=[mcp_server],
            model=OpenAIChatCompletionsModel(
                model=model_name,
                openai_client=client
            )
        )


    job_suggestions_agent = Agent(
            name="Job Suggestions",
            instructions=f"""You are a domain classifier that identifies the primary professional domain from a LinkedIn profile.
            """,
            model=OpenAIChatCompletionsModel(
                model=model_name,
                openai_client=client
            )
        )

    url_generator_agent = Agent(
            name="URL Generator",
            instructions=f"""You are a URL generator that creates Y Combinator job board URLs based on domains.
            """,
            model=OpenAIChatCompletionsModel(
                model=model_name,
                openai_client=client
            )
        )

    Job_search_agent = Agent(
            name="Job Finder",
            instructions=f"""You are a job finder that extracts job listings from Y Combinator's job board.
            """,
            mcp_servers=[mcp_server],
            model=OpenAIChatCompletionsModel(
                model=model_name,
                openai_client=client
            )
        )

    url_parser_agent = Agent(
            name="URL Parser",
            instructions=f"""You are a URL parser that transforms Y Combinator authentication URLs into direct job URLs.
            """,
            model=OpenAIChatCompletionsModel(
                model=model_name,
                openai_client=client
            )
        )

    summary_agent = Agent(
            name="Summary Agent",
            instructions=f"""You are a summary agent that creates comprehensive career analysis reports.

            Ensure your response is well-formatted markdown that can be directly displayed.""",
            model=OpenAIChatCompletionsModel(
                model=model_name,
                openai_client=client
            )
        )

# Get LinkedIn profile analysis
    logger.info("Running LinkedIn profile analysis")
    linkedin_result = await Runner.run(starting_agent=linkedin_agent, input=linkedin_url)
    logger.info("LinkedIn profile analysis completed")

    # Get job suggestions
    logger.info("Getting job suggestions")
    suggestions_result = await Runner.run(starting_agent=job_suggestions_agent, input=linkedin_result.final_output)
    logger.info("Job suggestions completed")

    # Get specific job matches
    logger.info("Getting job link")
    job_link_result = await Runner.run(starting_agent=url_generator_agent, input=suggestions_result.final_output)
    logger.info("Job link generation completed")

    # Get job matches
    logger.info("Getting job matches")
    job_search_result = await Runner.run(starting_agent=Job_search_agent, input=job_link_result.final_output)
    logger.info("Job search completed")

    # Parse URLs to get direct job links
    logger.info("Parsing job URLs")
    parsed_urls_result = await Runner.run(starting_agent=url_parser_agent, input=job_search_result.final_output)
    logger.info("URL parsing completed")

    # Create a single input for the summary agent
    logger.info("Generating final summary")
    summary_input = f"""LinkedIn Profile Analysis:
    {linkedin_result.final_output}

    Job Suggestions:
    {suggestions_result.final_output}

    Job Matches:
    {parsed_urls_result.final_output}

    Please analyze the above information and create a comprehensive career analysis report in markdown format."""

    # Get final summary with a single call
    summary_result = await Runner.run(starting_agent=summary_agent, input=summary_input)
    logger.info("Summary generation completed")
    return summary_result.final_output