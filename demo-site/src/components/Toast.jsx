import { useApp } from "../store.jsx";

export default function Toast() {
  const { toast } = useApp();
  return (
    <div
      id="toast"
      className={"toast" + (toast.visible ? " show" : "")}
      role="status"
      data-testid="toast-message"
      data-qa="toast"
    >
      {toast.message}
    </div>
  );
}
