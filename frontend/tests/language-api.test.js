import request from 'supertest';
import { app } from '../../backend/server.js';

describe('Language API endpoints', () => {
  it('detects language based on Accept-Language header', async () => {
    const res = await request(app)
      .get('/api/language/detect')
      .set('Accept-Language', 'he-IL');
    expect(res.statusCode).toBe(200);
    expect(res.body.language).toBe('he');
  });

  it('switches language successfully', async () => {
    const res = await request(app)
      .post('/api/language/switch')
      .send({ language: 'he' });
    expect(res.statusCode).toBe(200);
    expect(res.body.success).toBe(true);
  });

  it('rejects unsupported language switch', async () => {
    const res = await request(app)
      .post('/api/language/switch')
      .send({ language: 'fr' });
    expect(res.statusCode).toBe(400);
  });

  it('retrieves translations', async () => {
    const res = await request(app).get('/api/translations/he');
    expect(res.statusCode).toBe(200);
    expect(res.body.titleApp).toBeDefined();
  });
}); 