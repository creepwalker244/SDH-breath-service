from dataclasses import dataclass

@dataclass
class CalculationConstants:
    OneZ: float
    aZ: float
    bZ: float
    default_t: int
    default_p_base: int

constants = CalculationConstants(
    OneZ = 1,
    aZ = float('4.75e-04'),
    bZ = float('3.25e-07'),
    default_t = 23,
    default_p_base= 280
)

async def to_kalvins(celsius):
    if celsius:
        return celsius + 273
    else:
        return constants.default_t + 273

async def to_calculate_z(preasure:int):
    if not preasure:
        preasure = constants.default_p_base
    
    return constants.OneZ + (constants.aZ*preasure) - (constants.bZ*preasure**2)


async def to_calculate_target_temperature(
        preasure_1:int,
        preasure_2:int,
        z_preasure_1:float,
        z_preasure_2:float,
        temp_1:float
        
    )->float:
    if not preasure_1:
        preasure_1 = constants.default_p_base
    return (
        temp_1 * \
        (
            (preasure_2/z_preasure_2) \
            / (preasure_1/z_preasure_1)
        )
    )

async def to_calculate_volume(
        baloon_volume:float,
        preasure_2:int,
        temp1:float,
        temp2:float,
        z_preasure_2:float
    
    )->float:
    return (
        (
            (baloon_volume * preasure_2) \
            / z_preasure_2
        )
         * (temp1/temp2)
        )