import { Routes, Route } from 'react-router-dom';
import Menu from './pages/Menu.jsx';
import Admin from './pages/Admin.jsx';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Menu />} />
      <Route path="/admin" element={<Admin />} />
    </Routes>
  );
}
