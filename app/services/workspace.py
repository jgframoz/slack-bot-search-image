import datetime
from migrations.entities.workspaces import Workspace
from services.db import session
from services.aws import AwsService

class WorkspaceService:
    @staticmethod
    def create_workspace_if_not_exists(workspace_id: str) -> None:
        result = session.query(Workspace).filter(Workspace.workspace_identifier == workspace_id.lower()).all()

        if not result:
            workspace = Workspace(
                workspace_identifier = workspace_id.lower(),
                created_at = datetime.datetime.now()
            )
            
            # Create workspace
            session.add(workspace)
            session.commit()

            # Create S3 bucket
            try:
                AwsService.create_s3_bucket(workspace_id)
            except Exception as e:
                print('Error creating bucket', str(e))
