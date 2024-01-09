# new imports
from app.secure.secure import (authenticate_user, create_access_token,
                               fake_users_db)
from fastapi import APIRouter, Depends, Form, Request, responses, status
from fastapi.templating import Jinja2Templates

# from pydantic.error_wrappers import ValidationError


templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

# register  routes here


# @router.get("/token")
# def login(request: Request):
#    return templates.TemplateResponse("auth/login.html", {"request": request})
#
#
# @router.post("/token")
# def login(
#    request: Request,
#    username: str = Form(...),
#    password: str = Form(...),
# ):
#    errors = []
#    user = authenticate_user(fake_users_db, username=username, password=password)
#
#    if not user:
#        errors.append("Incorrect username or password")
#        return templates.TemplateResponse(
#            "auth/login.html", {"request": request, "errors": errors}
#        )
#    access_token = create_access_token(data={"sub": username})
#    print(access_token)
#    response = responses.RedirectResponse(
#        "/users/me", status_code=status.HTTP_302_FOUND
#    )
#    response.set_cookie(
#        key="access_token", value=f"Bearer {access_token}", httponly=True
#    )
#    return response
#
#
# @router.get("/")
# def default():
#    return {"default": 1}
