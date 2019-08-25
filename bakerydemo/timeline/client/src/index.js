import React, { Component } from 'react';

import Timeline from 'react-calendar-timeline';
import moment from 'moment';

// styles
import 'react-calendar-timeline/lib/Timeline.css'; // must include to ensure the timeline itself is styled
import './style.css';

const groups = [{ id: 1, title: 'group 1' }, { id: 2, title: 'group 2' }];

const items = [
  {
    id: 1,
    group: 1,
    title: 'item 1',
    start_time: moment(),
    end_time: moment().add(1, 'hour'),
  },
  {
    id: 2,
    group: 2,
    title: 'item 2',
    start_time: moment().add(-0.5, 'hour'),
    end_time: moment().add(0.5, 'hour'),
  },
  {
    id: 3,
    group: 1,
    title: 'item 3',
    start_time: moment().add(2, 'hour'),
    end_time: moment().add(3, 'hour'),
  },
];

export default class extends Component {
  constructor() {
    super();
    this.state = {
      isLoading: false,
      pages: [],
    };
  }

  componentDidMount() {
    const endpointUrl = '/api/v2/pages/?limit=200';
    fetch(endpointUrl)
      .then(function(response) {
        return response.json();
      })
      .then(function(myJson) {
        console.log(JSON.stringify(myJson));
      })
      .catch(error => console.log('error', error));
  }

  render() {
    return (
      <div className="timeline">
        <Timeline
          groups={groups}
          items={items}
          defaultTimeStart={moment().add(-12, 'hour')}
          defaultTimeEnd={moment().add(12, 'hour')}
        />
      </div>
    );
  }
}
