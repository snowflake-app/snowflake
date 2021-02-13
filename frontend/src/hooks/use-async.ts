import {useCallback, useEffect, useState} from "react";


type AsyncFunction<T> = () => Promise<T>
type State = 'idle' | 'pending' | 'success' | 'error';

export function useAsync<T>(asyncFn: AsyncFunction<T>) {
  const [status, setStatus] = useState<State>('idle');
  const [value, setValue] = useState<T | undefined>(undefined);
  const [error, setError] = useState(undefined);

  const execute = useCallback(async () => {
    setStatus('pending');
    setValue(undefined);

    try {
      const response = await asyncFn();
      setValue(response);
      setStatus('success');
    } catch (error) {
      setError(error);
      setStatus('error');
    }
  }, [asyncFn]);

  useEffect(() => {
    (async () => await execute())();
  }, [execute]);

  return {status, value, error};
}
