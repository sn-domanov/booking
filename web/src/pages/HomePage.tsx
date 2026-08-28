import ListingListContainer from "@/entities/listing/ui/ListingListContainer";

function HomePage() {
  return (
    <section className="page py-8 space-y-4">
      <h1>Welcome to Booking!</h1>

      <ListingListContainer />
    </section>
  );
}

export default HomePage;
