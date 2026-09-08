import { useAuth } from "@/app/providers/auth/useAuth";
import ListingListContainer from "@/entities/listing/ui/ListingListContainer";

function HomePage() {
  const { user } = useAuth();

  return (
    <section className="page py-8 space-y-4">
      <h1>Welcome to Booking{user ? `, ${user.displayName}` : ""}!</h1>

      <ListingListContainer />
    </section>
  );
}

export default HomePage;
