import React, {ComponentProps, createContext, useContext, useState} from "react";

type Category = "primary" | "link" | "info" | "success" | "warning" | "danger";

type Alert = {
  id: string
  title: string,
  category?: Category
  content: string
}

type AddAlertProps = {
  id?: string,
  title: string,
  category: Category,
  content: string
};

type AlertContext = {
  alerts: Alert[]
  addAlert: (notification: AddAlertProps) => void,
  removeAlert: (id: string) => void
};

const noopAlertContext: AlertContext = {
  alerts: [],
  addAlert: _ => {
  },
  removeAlert: _ => {
  }
};

const notificationContext = createContext<AlertContext>(noopAlertContext);

export function AlertProvider({children}: ComponentProps<any>) {
  const context = useProvideAlerts();
  return (<notificationContext.Provider value={context}>{children}</notificationContext.Provider>);
}

export const useAlerts = () => {
  return useContext(notificationContext);
};

function generateRandomId() {
  return "n_" + Date.now().toString(36)
}

function useProvideAlerts(): AlertContext {

  const [alerts, setAlerts] = useState<Alert[]>([]);

  const addAlert = (notification: AddAlertProps) => {
    const id = notification.id || generateRandomId();
    setAlerts(prevState => [...prevState, {id, ...notification}]);
    setTimeout(() => removeAlert(id), 10000);
  };

  const removeAlert = (id: string) => {
    setAlerts(prevState => prevState.filter(value => value.id !== id))
  };

  return {alerts, addAlert, removeAlert};
}

