import { navigate } from "gatsby";
import { useLocation } from "@gatsbyjs/reach-router";
import React, { useEffect, useMemo, useState } from "react";
import Layout from "../../components/Layout";
import { createRental, listActiveCars } from "../../api/client";
import { useAuth } from "../../context/AuthContext";
import { formatCurrency } from "../../utils/format";

const NovaReservaPage = () => {
  const { user, loading: authLoading } = useAuth();
  const location = useLocation();
  const [cars, setCars] = useState([]);
  const [loadingCars, setLoadingCars] = useState(true);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});
  const [form, setForm] = useState({
    car: "",
    start_date: "",
    end_date: "",
    agreed_daily_rate: "",
    pickup_location: "",
    return_location: "",
    notes: "",
  });

  const preselectedCarId = useMemo(() => {
    const params = new URLSearchParams(location?.search || "");
    return params.get("car");
  }, [location]);

  useEffect(() => {
    if (!authLoading && !user) {
      navigate("/login/?next=/rentals/nova/");
    }
  }, [authLoading, user]);

  useEffect(() => {
    if (authLoading || !user) {
      return;
    }
    let cancelled = false;

    const loadCars = async () => {
      setLoadingCars(true);
      setError(null);
      try {
        const response = await listActiveCars();
        if (!cancelled) {
          const items = response.results || response || [];
          setCars(items);
          if (items.length > 0) {
            const matchingCar = items.find(
              (item) => item.id === preselectedCarId
            );
            if (matchingCar) {
              setForm((previous) => ({
                ...previous,
                car: matchingCar.id,
                agreed_daily_rate: matchingCar.daily_rate,
              }));
            }
          }
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Não foi possível carregar os carros.");
        }
      } finally {
        if (!cancelled) {
          setLoadingCars(false);
        }
      }
    };

    loadCars();
    return () => {
      cancelled = true;
    };
  }, [authLoading, user, preselectedCarId]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((previous) => {
      const next = { ...previous, [name]: value };
      if (name === "car") {
        const selected = cars.find((car) => car.id === value);
        if (selected) {
          next.agreed_daily_rate = selected.daily_rate;
        }
      }
      return next;
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    setFieldErrors({});

    const payload = {
      car: form.car,
      start_date: form.start_date,
      end_date: form.end_date,
      agreed_daily_rate: form.agreed_daily_rate,
      pickup_location: form.pickup_location,
      return_location: form.return_location,
      notes: form.notes,
    };

    try {
      await createRental(payload);
      navigate("/?success=on");
    } catch (err) {
      if (err.payload && typeof err.payload === "object") {
        setFieldErrors(err.payload);
      }
      setError(err.message || "Não foi possível criar a reserva.");
    } finally {
      setSubmitting(false);
    }
  };

  const renderFieldError = (name) => {
    const value = fieldErrors?.[name];
    if (!value) {
      return null;
    }
    const messages = Array.isArray(value) ? value : [value];
    return messages.map((message, index) => (
      <p key={`${name}-${index}`} className="alert alert--error">
        {message}
      </p>
    ));
  };

  return (
    <Layout>
      <section className="card">
        <h2 className="card__title">Criar reserva</h2>
        <p className="card__meta">
          Selecione um carro disponível e informe o período desejado.
        </p>
        {error && <p className="alert alert--error">{error}</p>}
        {renderFieldError("non_field_errors")}
        {renderFieldError("detail")}
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="car">Carro</label>
            <select
              id="car"
              name="car"
              value={form.car}
              onChange={handleChange}
              required
              disabled={loadingCars || submitting}
            >
              <option value="" disabled>
                {loadingCars ? "Carregando..." : "Selecione um carro"}
              </option>
              {cars.map((car) => (
                <option key={car.id} value={car.id}>
                  {car.brand} {car.model} ({car.plate}) ·{" "}
                  {formatCurrency(car.daily_rate)} / dia
                </option>
              ))}
            </select>
            {renderFieldError("car")}
          </div>

          <div>
            <label htmlFor="start_date">Data de início</label>
            <input
              id="start_date"
              name="start_date"
              type="date"
              value={form.start_date}
              onChange={handleChange}
              required
              disabled={submitting}
            />
            {renderFieldError("start_date")}
          </div>

          <div>
            <label htmlFor="end_date">Data de término</label>
            <input
              id="end_date"
              name="end_date"
              type="date"
              value={form.end_date}
              onChange={handleChange}
              required
              disabled={submitting}
            />
            {renderFieldError("end_date")}
          </div>

          <div>
            <label htmlFor="agreed_daily_rate">Valor por dia</label>
            <input
              id="agreed_daily_rate"
              name="agreed_daily_rate"
              type="number"
              min="0"
              step="0.01"
              value={form.agreed_daily_rate}
              onChange={handleChange}
              required
              disabled={submitting}
            />
            {renderFieldError("agreed_daily_rate")}
          </div>

          <div>
            <label htmlFor="pickup_location">Retirada</label>
            <input
              id="pickup_location"
              name="pickup_location"
              type="text"
              value={form.pickup_location}
              onChange={handleChange}
              disabled={submitting}
            />
            {renderFieldError("pickup_location")}
          </div>

          <div>
            <label htmlFor="return_location">Devolução</label>
            <input
              id="return_location"
              name="return_location"
              type="text"
              value={form.return_location}
              onChange={handleChange}
              disabled={submitting}
            />
            {renderFieldError("return_location")}
          </div>

          <div>
            <label htmlFor="notes">Notas</label>
            <textarea
              id="notes"
              name="notes"
              rows={3}
              value={form.notes}
              onChange={handleChange}
              disabled={submitting}
            />
            {renderFieldError("notes")}
          </div>

          <div className="form__actions">
            <button type="submit" className="button" disabled={submitting}>
              {submitting ? "Salvando..." : "Confirmar reserva"}
            </button>
            <button
              type="button"
              className="button button--secondary"
              onClick={() => navigate("/")}
              disabled={submitting}
            >
              Cancelar
            </button>
          </div>
        </form>
      </section>
    </Layout>
  );
};

export default NovaReservaPage;
