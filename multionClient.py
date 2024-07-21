from multion.client import MultiOn
import os 

client = MultiOn(
    api_key=os.environ.get("MULTION_API_KEY")
)


def getMultiOnResponse(topic):

    create_response = client.sessions.create(
        url="https://www.youtube.com/",
        local=True,
        use_proxy=True,
        mode="fast"
    )

    result1 = client.browse(session_id=create_response.session_id,
    cmd="Navigate to the Search bar and type {topic}.")

    step_response = client.sessions.step(
        session_id=result1.session_id,
        cmd="click on the first YouTube video."
    )
    retrieve_response = client.retrieve(
        session_id=step_response.session_id,
        cmd="Get the url of page"
    )
    client.sessions.close(
        session_id=retrieve_response.session_id,
    )


    youtube_url = retrieve_response.url
    return youtube_url