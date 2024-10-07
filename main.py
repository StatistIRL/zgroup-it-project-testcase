import dotenv
import uvicorn

from settings import ApplicationSettings, get_settings

if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    settings: ApplicationSettings = get_settings(ApplicationSettings)
    uvicorn.run(
        "api.app:create_app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        factory=True,
    )
