type Props = {
    name: string;
    type: string;
    value: string;
    placeholder: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
};

const Input = ({ name, type, value, placeholder, onChange }: Props) => {
    return (
        <div className="relative h-full w-full">
            <input
                name={name}
                type={type}
                value={value}
                placeholder={placeholder}
                autoComplete="false"
                className="peer/input-field h-full w-full rounded border-[1px] p-2 text-gray-500 outline-none placeholder:text-sm focus:outline-none focus:ring-1 focus:ring-gray-400 focus:placeholder:text-transparent"
                onChange={onChange}
            />
            <span className="absolute -top-[10px] left-[10px] hidden bg-white text-sm text-gray-400 peer-focus/input-field:block">
                {placeholder}
            </span>
        </div>
    );
};

export default Input;
