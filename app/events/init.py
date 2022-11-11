import os

from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient

from services.workspace import WorkspaceService
from events.file_share import upload_files

client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))

def init(event):
    workspace_id = event['team']
    channel_id = event['channel']
    channel_type = 'channel' if event['channel_type'] == 'C' else event['channel_type']

    conversation_id = None

    # Create workspace instance and S3 bucket
    WorkspaceService.create_workspace_if_not_exists(workspace_id)

    try:
        # Call the conversations.list method using the WebClient
        for result in client.conversations_list():
            if conversation_id is not None:
                break
            for channel in result["channels"]:
                if channel["id"] == channel_id:
                    conversation_id = channel["id"]
                    #Print result
                    print(f"Found conversation ID: {conversation_id}")
                    break

    except SlackApiError as e:
        print(f"Error (init for workspace {workspace_id}): {e}")

    try:
        # Call the conversations.history method using the WebClient
        # conversations.history returns the first 100 messages by default
        # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination

        lastTimestamp = None

        while(True): #change in the future to lastTimestamp < date 
            response = client.conversations_history(channel=conversation_id, latest=lastTimestamp)

            for m in response['messages']:
                if 'files' in m.keys():
                    upload_files({**m, 'channel_type': channel_type}, is_init=True, c_id=conversation_id)
                
            if (response['has_more']):
                lastTimestamp = response['messages'][-1]['ts']
            else:
                break
        return 'ok'

    except SlackApiError as e:
        print(f'ERROR (list and upload files for workspace {workspace_id}): creating conversation: {e}')