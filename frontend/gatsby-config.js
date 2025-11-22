const apiUrl = process.env.GATSBY_API_URL || "http://localhost:8000";

module.exports = {
  siteMetadata: {
    title: "Car Rental Portal",
    description: "Dashboard Gatsby para reservas de veículos",
    author: "Car Rental",
    apiUrl,
  },
  graphqlTypegen: true,
};
