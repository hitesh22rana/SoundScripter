type CircularProgressProps = {
    width: string;
    height: string;
    centerOfRotation: string;
    children: React.ReactNode;
};

type CircleProps = {
    radius: number;
    centerX: number;
    centerY: number;
    fill: string;
    stroke: string;
    strokeWidth: string;
    percentage: number;
};

const Circle = ({
    radius,
    centerX,
    centerY,
    fill,
    stroke,
    strokeWidth,
    percentage,
}: CircleProps) => {
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = ((100 - percentage) * circumference) / 100;

    return (
        <circle
            r={radius}
            cx={centerX}
            cy={centerY}
            fill={fill}
            stroke={stroke}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
        />
    );
};

const CircularProgress = ({
    width,
    height,
    centerOfRotation,
    children,
}: CircularProgressProps) => {
    return (
        <svg width={width} height={height}>
            <g transform={centerOfRotation}>{children}</g>
        </svg>
    );
};

export { Circle, CircularProgress };
