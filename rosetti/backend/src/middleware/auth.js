const ADMIN_USER = process.env.ADMIN_USER || 'admin';
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'rosetti123';

export function requireAdminAuth(req, res, next) {
  const header = req.headers.authorization || '';
  const [scheme, encoded] = header.split(' ');

  if (scheme !== 'Basic' || !encoded) {
    res.set('WWW-Authenticate', 'Basic realm="Rosetti Admin"');
    return res.status(401).json({ error: 'Autenticação necessária' });
  }

  const decoded = Buffer.from(encoded, 'base64').toString('utf-8');
  const separatorIndex = decoded.indexOf(':');
  const user = decoded.slice(0, separatorIndex);
  const password = decoded.slice(separatorIndex + 1);

  if (user !== ADMIN_USER || password !== ADMIN_PASSWORD) {
    res.set('WWW-Authenticate', 'Basic realm="Rosetti Admin"');
    return res.status(401).json({ error: 'Usuário ou senha inválidos' });
  }

  next();
}
