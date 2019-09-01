/* eslint-disable import/no-extraneous-dependencies */
import { render } from 'react-dom';
import HelloWorld from './components/HelloWorld';
import Timeline from './components/Timeline';

const root = document.getElementById('root');

render(
  <div>
    <HelloWorld />
    <Timeline />
  </div>,
  root,
);
