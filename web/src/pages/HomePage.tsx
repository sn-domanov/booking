import { useAuth } from "@/app/providers/auth/useAuth";
import ListingListContainer from "@/entities/listing/ui/ListingListContainer";

function HomePage() {
  const { user } = useAuth();

  return (
    <section className="page space-y-4 py-8">
      <h1>Welcome to Booking{user ? `, ${user.displayName}` : ""}!</h1>

      <ListingListContainer />
    </section>
  );
}

export default HomePage;
