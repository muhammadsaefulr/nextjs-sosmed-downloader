import React from "react";

interface ToastAlertProps {
    message: string;
  }

export const ToastAlert: React.FC<ToastAlertProps> = ({ message }) => {
  return (
    <div className="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-md shadow-lg">
      {message}
    </div>
  );
};
