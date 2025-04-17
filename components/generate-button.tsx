import { FC } from 'react';
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export interface GenerateButtonProps {
  onClick: () => Promise<void>;
  isGenerating: boolean;
  disabled: boolean;
  className?: string;
}

export const GenerateButton: FC<GenerateButtonProps> = ({
  onClick,
  isGenerating,
  disabled,
  className
}) => {
  return (
    <Button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "h-[52px] px-8 rounded-2xl",
        "bg-gradient-to-r from-blue-600 to-purple-600",
        "hover:from-blue-700 hover:to-purple-700",
        "transition-all duration-300",
        "hover:shadow-lg hover:-translate-y-0.5",
        "disabled:opacity-50 disabled:hover:translate-y-0",
        "text-lg font-medium",
        className
      )}
    >
      {isGenerating ? "Generating..." : "Generate"}
    </Button>
  );
}; 