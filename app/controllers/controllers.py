from app.models.models import CalculationParamsCreate
from app.models.db import CalculationParams
from app.controllers.functions import *
from app.configs.connection import SingletoneDBConnection, DBCONN

class CalculationParamsCreateController:

    @staticmethod
    async def calculate_true_preasure(calculation_params: CalculationParamsCreate, dbcon: SingletoneDBConnection = DBCONN):
        
        db_calculation_params = CalculationParams(**calculation_params.model_dump())

        db_calculation_params.storage_temperature = await to_kalvins(db_calculation_params.storage_temperature)
        db_calculation_params.z_value_base = await to_calculate_z(db_calculation_params.base_pressure)
        db_calculation_params.z_value_work = await to_calculate_z(db_calculation_params.work_pressure)
        db_calculation_params.target_temperature = await to_calculate_target_temperature(
            db_calculation_params.base_pressure, 
            db_calculation_params.work_pressure,
            db_calculation_params.z_value_base,
            db_calculation_params.z_value_work,
            db_calculation_params.storage_temperature
            )
        db_calculation_params.true_volume = await to_calculate_volume(
            db_calculation_params.baloon_volume, 
            db_calculation_params.work_pressure, 
            db_calculation_params.storage_temperature, 
            db_calculation_params.target_temperature,
            db_calculation_params.z_value_work
            )

        return db_calculation_params
