import { FC, KeyboardEvent, Dispatch, SetStateAction } from 'react';
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

export interface SearchInputProps {
  value: string;
  onChange: Dispatch<SetStateAction<string>>;
  onKeyDown: (e: KeyboardEvent<HTMLInputElement>) => void;
  isGenerating: boolean;
  placeholder?: string;
  className?: string;
}

export const SearchInput: FC<SearchInputProps> = ({
  value,
  onChange,
  onKeyDown,
  isGenerating,
  placeholder = "Search...",
  className
}) => {
  return (
    <Input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onKeyDown={onKeyDown}
      disabled={isGenerating}
      placeholder={placeholder}
      className={cn(
        "w-full h-full min-h-[52px] text-lg rounded-2xl border-2",
        "border-gray-200 dark:border-gray-700",
        "focus:border-blue-500 dark:focus:border-blue-400",
        "transition-all duration-300",
        "bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm",
        className
      )}
    />
  );
}; 