from fastapi import BackgroundTasks, APIRouter

router = APIRouter()

def write_notification(email: str, message = ""):
    with open("log.txt", mode = "a") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content + "\n")
    
@router.post("/send-notification/{email}")    
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background", "email": email}

### Dependency Injection Case ###
from typing import Annotated
from fastapi import Depends

def write_log(message: str):
    with open("log.txt", mode="a") as log_file:
        log_file.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@router.post("/send-notification/DepInj/{email}")
async def send_notification_dep_inj(
    email: str,
    background_tasks: BackgroundTasks,
    q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}