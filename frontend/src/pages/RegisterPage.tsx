import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import { registerUser } from "../api/auth";
import type { RegisterData, FormErrors } from "../types";

export default function RegisterPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState<RegisterData>({
    username: "",
    email: "",
    password: "",
    password2: "",
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: "" });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    try {
      const data = await registerUser(form);
      login(data.user, { access: data.access, refresh: data.refresh });
      navigate("/");
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.data) {
        setErrors(err.response.data);
      }
    } finally {
      setLoading(false);
    }
  };

  interface FormField {
    name: keyof RegisterData;
    label: string;
    type: string;
    placeholder: string;
  }

  const fields: FormField[] = [
    {
      name: "username",
      label: "Username",
      type: "text",
      placeholder: "your_username",
    },
    {
      name: "email",
      label: "Email",
      type: "email",
      placeholder: "juan@email.com",
    },
    {
      name: "password",
      label: "Password",
      type: "password",
      placeholder: "••••••••",
    },
    {
      name: "password2",
      label: "Confirm Password",
      type: "password",
      placeholder: "••••••••",
    },
  ];

  return (
    <div className="container mt-4">
      <div className="row justify-content-center">
        <div className="col-md-5">
          <div className="card shadow-sm">
            <div className="card-body p-4">
              <h3 className="mb-4">Create Account</h3>

              {errors.non_field_errors && (
                <div className="alert alert-danger">
                  {errors.non_field_errors}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                {fields.map((field) => (
                  <div className="mb-3" key={field.name}>
                    <label className="form-label fw-semibold">
                      {field.label}
                    </label>
                    <input
                      type={field.type}
                      name={field.name}
                      className={`form-control ${errors[field.name] ? "is-invalid" : ""}`}
                      placeholder={field.placeholder}
                      value={form[field.name]}
                      onChange={handleChange}
                      required
                    />
                    {errors[field.name] && (
                      <div className="invalid-feedback">
                        {Array.isArray(errors[field.name])
                          ? errors[field.name][0]
                          : errors[field.name]}
                      </div>
                    )}
                  </div>
                ))}

                <button
                  type="submit"
                  className="btn btn-dark w-100 mt-2"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" />
                      Creating account...
                    </>
                  ) : (
                    "Register"
                  )}
                </button>
              </form>

              <p className="text-center mt-3 mb-0">
                Already have an account? <Link to="/login">Login</Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
