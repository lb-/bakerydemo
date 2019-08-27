import React, { Component } from 'react';
import { render } from 'react-dom';

import Example from '../../src';

class Demo extends Component {
  render() {
    return (
      <div>
        <h1>client Demo</h1>
        <form action="/admin/timeline/" method="get" role="search">
          <label htmlFor="id_q">Search term:</label>
          <input type="text" name="q" id="id_q" placeholder="Search" />
        </form>
        <Example searchFormId="id_q" />
      </div>
    );
  }
}

render(<Demo />, document.querySelector('#demo'));
