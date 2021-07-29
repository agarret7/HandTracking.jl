using StaticArrays: SVector

struct UnitQuaternion
end

function quat2euler(q::UnitQuaternion)
end

function euler2quat()
end

struct Joint
    scale::Real
    orn::UnitQuaternion
end

const Finger = SVector{3,Joint}

struct Hand
    scale::SVector{3,<:Real}
    pos::SVector{3,<:Real}
    orn::UnitQuaternion
end
