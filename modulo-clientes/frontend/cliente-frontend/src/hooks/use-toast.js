import { toast as sonnerToast } from "sonner";

/**
 * Hook customizado para exibir notificações (toasts) usando a biblioteca Sonner.
 * Ele replica a API do useToast do shadcn/ui para compatibilidade.
 */
export const useToast = () => {
  const toast = ({ title, description, variant, ...props }) => {
    if (variant === "destructive") {
      sonnerToast.error(title, {
        description,
        ...props,
      });
    } else {
      sonnerToast.success(title, {
        description,
        ...props,
      });
    }
  };

  return { toast };
};
