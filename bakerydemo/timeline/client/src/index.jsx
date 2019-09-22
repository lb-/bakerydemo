import { render } from 'react-dom'; // eslint-disable-line import/no-extraneous-dependencies
import Timeline from './components/Timeline';

const root = document.getElementById('root');

render(
  <main>
    <h1>Demo</h1>
    <form action="/admin/timeline/" method="get" role="search">
      <label htmlFor="id_q">
        Search term:
        <input type="text" name="q" id="id_q" placeholder="Search" />
      </label>
    </form>
    <Timeline searchFormId="id_q" />
  </main>,
  root,
);
