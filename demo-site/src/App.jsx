import { Navigate, Outlet, Route, Routes } from "react-router-dom";
import { useApp } from "./store.jsx";
import Header from "./components/Header.jsx";
import Toast from "./components/Toast.jsx";
import Login from "./pages/Login.jsx";
import Products from "./pages/Products.jsx";
import ProductDetail from "./pages/ProductDetail.jsx";
import Cart from "./pages/Cart.jsx";
import Contact from "./pages/Contact.jsx";

function ProtectedLayout() {
  const { user, t } = useApp();
  if (!user) return <Navigate to="/login" replace />;
  return (
    <>
      <Header />
      <main className="container">
        <Outlet />
      </main>
      <footer className="site-footer" data-testid="site-footer">{t("footer")}</footer>
    </>
  );
}

export default function App() {
  const { user } = useApp();
  return (
    <>
      <Routes>
        <Route path="/login" element={user ? <Navigate to="/products" replace /> : <Login />} />
        <Route element={<ProtectedLayout />}>
          <Route path="/products" element={<Products />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/contact" element={<Contact />} />
        </Route>
        <Route path="*" element={<Navigate to={user ? "/products" : "/login"} replace />} />
      </Routes>
      <Toast />
    </>
  );
}
