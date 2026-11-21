"""Press Run to render all seven chapters. Settings live in settings.py."""
import os
from film_core import render_chapter
from scene_01_opening import Scene01Opening
from scene_02_speed_velocity import Scene02SpeedVelocity
from scene_03_acceleration_definition import Scene03AccelerationDefinition
from scene_04_acceleration_braking import Scene04AccelerationBraking
from scene_05_changing_direction import Scene05ChangingDirection
from scene_06_uniform_circular_motion import Scene06UniformCircularMotion
from scene_07_centripetal_acceleration import Scene07CentripetalAcceleration

SCENES=[Scene01Opening,Scene02SpeedVelocity,Scene03AccelerationDefinition,
        Scene04AccelerationBraking,Scene05ChangingDirection,
        Scene06UniformCircularMotion,Scene07CentripetalAcceleration]

if __name__=="__main__":
    os.environ["PHYSICS_BATCH"]="1"
    for scene in SCENES:
        render_chapter(scene)
