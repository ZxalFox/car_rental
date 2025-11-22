import { useLocation } from "@gatsbyjs/reach-router";
import { Link, navigate } from "gatsby";
import React, { useEffect, useMemo, useState } from "react";
import Layout from "../components/Layout";
import { listActiveCars, listMyRentals } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { formatCurrency, formatDate } from "../utils/format";

const statusLabel = {
  reserved: "Reservada",
  ongoing: "Em curso",
  finished: "Finalizada",
  canceled: "Cancelada",
};

const IndexPage = () => {
  const { user, loading: authLoading } = useAuth();
  const location = useLocation();
  const [cars, setCars] = useState([]);
  const [rentals, setRentals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reservationCreated, setReservationCreated] = useState(false);

  useEffect(() => {
    if (!location) {
      return;
    }
    const params = new URLSearchParams(location.search || "");
    if (params.get("success") === "on") {
      setReservationCreated(true);
      if (typeof window !== "undefined") {
        params.delete("success");
        const query = params.toString();
        const nextPath = `${window.location.pathname}${
          query ? `?${query}` : ""
        }`;
        window.history.replaceState({}, "", nextPath);
      }
    }
  }, [location]);

  useEffect(() => {
    if (!authLoading && !user) {
      navigate("/login/");
    }
  }, [authLoading, user]);

  useEffect(() => {
    if (authLoading || !user) {
      return;
    }

    let cancelled = false;

    const loadDashboard = async () => {
      setLoading(true);
      setError(null);
      try {
        const [carsResponse, rentalsResponse] = await Promise.all([
          listActiveCars(),
          listMyRentals(),
        ]);
        if (!cancelled) {
          setCars(carsResponse.results || carsResponse || []);
          setRentals(rentalsResponse.results || rentalsResponse || []);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Não foi possível carregar os dados.");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    loadDashboard();
    return () => {
      cancelled = true;
    };
  }, [authLoading, user]);

  const rentalsSummary = useMemo(
    () =>
      rentals.map((rental) => ({
        id: rental.id,
        carName: [rental.car_detail?.brand, rental.car_detail?.model]
          .filter(Boolean)
          .join(" "),
        carPlate: rental.car_detail?.plate,
        period: `${formatDate(rental.start_date)} → ${formatDate(
          rental.end_date
        )}`,
        status: rental.status,
        total: formatCurrency(rental.total_price),
      })),
    [rentals]
  );

  return (
    <Layout>
      <section className="dashboard">
        <article className="card">
          <h2 className="card__title">Resumo</h2>
          <p className="card__meta">
            Gerencie reservas e encontre veículos disponíveis com o novo
            frontend Gatsby.
          </p>
          <p className="card__meta">Reservas ativas: {rentals.length}</p>
          {reservationCreated && (
            <p className="alert">Reserva criada com sucesso.</p>
          )}
        </article>

        <article className="card">
          <div className="card__header">
            <h2 className="card__title">Minhas reservas</h2>
            <div className="card__actions">
              <Link className="card__button" to="/rentals/nova/">
                Nova reserva
              </Link>
            </div>
          </div>
          {loading && <p>Carregando dados...</p>}
          {error && <p className="alert alert--error">{error}</p>}
          {!loading && !error && rentalsSummary.length === 0 && (
            <p>Você ainda não possui reservas. Experimente criar a primeira.</p>
          )}
          {!loading && !error && rentalsSummary.length > 0 && (
            <table>
              <thead>
                <tr>
                  <th>Carro</th>
                  <th>Período</th>
                  <th>Status</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                {rentalsSummary.map((rental) => (
                  <tr key={rental.id}>
                    <td>
                      {rental.carName || "-"}
                      {rental.carPlate ? ` (${rental.carPlate})` : ""}
                    </td>
                    <td>{rental.period}</td>
                    <td>{statusLabel[rental.status] || rental.status}</td>
                    <td>{rental.total}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </article>

        <article className="card">
          <h2 className="card__title">Carros disponíveis</h2>
          {loading && <p>Carregando carros...</p>}
          {!loading && cars.length === 0 && <p>Não há veículos ativos.</p>}
          {!loading && cars.length > 0 && (
            <div className="cards-grid">
              {cars.map((car) => (
                <article key={car.id} className="card">
                  <h3 className="card__title">
                    {car.brand} {car.model}
                  </h3>
                  <p className="card__meta">Placa {car.plate}</p>
                  <p className="card__meta">Ano {car.year}</p>
                  <p className="card__meta">
                    Diária: {formatCurrency(car.daily_rate)}
                  </p>
                  <p className="card__meta">Quilometragem: {car.odometer} km</p>
                  <div className="card__actions">
                    <Link
                      className="card__button"
                      to={`/rentals/nova/?car=${car.id}`}
                    >
                      Reservar
                    </Link>
                  </div>
                </article>
              ))}
            </div>
          )}
        </article>
      </section>
    </Layout>
  );
};

export default IndexPage;
