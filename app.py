import uvicorn

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from supertokens_python import init, get_all_cors_headers
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.multitenancy.asyncio import list_all_tenants
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.userroles import UserRoleClaim

import config

init(
    supertokens_config=config.supertokens_config,
    app_info=config.app_info,
    framework=config.framework,
    recipe_list=config.recipe_list,
    mode="asgi",
)


app = FastAPI(title="SuperTokens example")

app.add_middleware(get_middleware())

@app.get("/sessioninfo")    
async def secure_api(s: SessionContainer = Depends(verify_session())):
    return {
        "sessionHandle": s.get_handle(),
        "userId": s.get_user_id(),
        "accessTokenPayload": s.get_access_token_payload(),
    }

@app.get('/delete_all')  
async def delete_all(session: SessionContainer = Depends(
        verify_session(
            # We add the UserRoleClaim's includes validator
            override_global_claim_validators=lambda global_validators, session, user_context: global_validators + \
            [UserRoleClaim.validators.includes("admin")]
        )
)):
    return {
        "status": "OK",
    }

@app.get('/update_user')  
async def update_user(session: SessionContainer = Depends(
        verify_session(
            # We add the UserRoleClaim's includes validator
            override_global_claim_validators=lambda global_validators, session, user_context: global_validators + \
            [UserRoleClaim.validators.includes("user")]
        )
)):
    return {
        "status": "OK",
    }


app = CORSMiddleware(
    app=app,
    allow_origins=[config.app_info.website_domain],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)


if __name__  == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
