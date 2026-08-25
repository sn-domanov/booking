import { useEffect } from "react";

import { checkHealth } from "@/shared/api/health";

function App() {
  useEffect(() => {
    checkHealth().then(console.log).catch(console.error);
  }, []);

  return <h1>Welcome to Booking!</h1>;
}

export default App;
