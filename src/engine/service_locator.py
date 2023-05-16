from src.engine.services.fonts_service import FontsService
from src.engine.services.images_service import ImagesService
from src.engine.services.sounds_service import SoundsService
from src.engine.services.setting_service import SettingService


class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsService()
    fonts_service = FontsService()
    setting_service = SettingService()
