from agents import (
    writer_chain,
    critic_chain
)

from tools import search_web, scrape_web

from rich import print


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # ==================================================
    # STEP 1: SEARCH
    # ==================================================

    print("\n" + "=" * 50)
    print("Step 1: Searching for relevant information...")
    print("=" * 50)

    # Direct Tavily search
    search_results = search_web.invoke(topic)

    state["search_results"] = search_results

    print("\nSearch Results:\n")

    for idx, result in enumerate(search_results, start=1):

        print(f"\n[{idx}] {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}")

    # ==================================================
    # STEP 2: SCRAPE REAL URLS
    # ==================================================

    print("\n" + "=" * 50)
    print("Step 2: Scraping top sources...")
    print("=" * 50)

    scraped_contents = []

    # Scrape top 3 results
    for result in search_results[:3]:

        url = result["url"]

        print(f"\nScraping: {url}")

        content = scrape_web.invoke(url)

        scraped_contents.append(
            f"\nSOURCE URL: {url}\n\n{content}"
        )

    state["reader_insights"] = "\n\n".join(scraped_contents)

    print("\nScraping completed successfully.")

    # ==================================================
    # STEP 3: WRITER
    # ==================================================

    print("\n" + "=" * 50)
    print("Step 3: Writing final report...")
    print("=" * 50)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n{state['reader_insights']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nGenerated Report:\n")
    print(state["report"])

    # ==================================================
    # STEP 4: CRITIC
    # ==================================================

    print("\n" + "=" * 50)
    print("Step 4: Critiquing report...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic Feedback:\n")
    print(state["feedback"])

    return state


if __name__ == "__main__":

    topic = input("\nEnter a research topic: ")

    run_research_pipeline(topic)