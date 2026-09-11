import { Link } from "react-router-dom";

import { Button } from "@/shared/components/ui/button";

function GuestNav() {
  return (
    <>
      <Button
        variant="ghost"
        render={<Link to="/login" />}
        nativeButton={false}
      >
        Log in
      </Button>

      <Button render={<Link to="/signup" />} nativeButton={false}>
        Sign up
      </Button>
    </>
  );
}

export default GuestNav;
