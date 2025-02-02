import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

interface IDialogWithButtonProps {
  buttonText: string;
  title: string;
  description: object;
  type: string;
}

export default function DialogWithButton({
  buttonText,
  title,
  description,
  type,
}: IDialogWithButtonProps) {
  return (
    <>
      <Dialog>
        <DialogTrigger>
          <Button>{buttonText}</Button>
        </DialogTrigger>
        <DialogContent className="w-[90vw] min-h-[50vh] rounded-xl">
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
            <DialogDescription className="text-left overflow-y-scroll max-h-[65vh]">
              {type === "interactions" &&
                Object.entries(description).map(([key, value]) => (
                  <li key={key}>
                    <strong>{key}:</strong>{" "}
                    {Object.entries(value).map(([k, v]) => (
                      <li key={k}>
                        <strong>{k}:</strong> {v as string}
                      </li>
                    ))}
                  </li>
                ))}

              {type === "sideEffects" &&
                Object.entries(description).map(([key, values]) => (
                  <div key={key}>
                    <strong>{key}:</strong>
                    <ul>
                      {values.map((value: string, index: number) => (
                        <li key={index}>{value}</li>
                      ))}
                    </ul>
                  </div>
                ))}
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </>
  );
}
