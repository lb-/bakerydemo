// timeline/client/src/index.jsx

import React from 'react';
import { render } from 'react-dom';
import Timeline from './components/Timeline';

render(
  <main className="main">
    <header role="banner">
      <div className="row nice-padding">
        <div className="left">
          <div className="col header-title">
            <h1 className="icon icon-">Timeline</h1>
          </div>
        </div>
        <div className="right" />
      </div>
    </header>
    <Timeline className="additional-class" />
  </main>,
  document.getElementById('root'),
);
