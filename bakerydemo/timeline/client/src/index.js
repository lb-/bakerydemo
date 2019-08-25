import React, { Component } from 'react';

import Timeline from 'react-calendar-timeline';
import moment from 'moment';

// styles
import 'react-calendar-timeline/lib/Timeline.css'; // must include to ensure the timeline itself is styled
import './style.css';

export default class extends Component {
  constructor() {
    super();
    this.state = {
      defaultTimes: {},
      error: null,
      groups: [],
      isLoading: true,
      items: [],
    };
  }

  componentDidMount() {
    const endpointUrl = '/api/v2/pages/?limit=200';
    this.setState({ isLoading: true });
    fetch(endpointUrl)
      .then(response => response.json())
      .then(response => {
        const items = this.getTransformedItems(response);

        console.log('result', {
          defaultTimes: this.getDefaultTimes(items),
          error: null,
          groups: this.getGroups(items),
          isLoading: false,
          items,
        });

        this.setState({
          defaultTimes: this.getDefaultTimes(items),
          error: null,
          groups: this.getGroups(items),
          isLoading: false,
          items,
        });
      })
      .catch(error => this.setState({ error, isLoading: false }));
  }

  getTransformedItems = ({ items = [] } = {}) =>
    items.map(({ meta: { first_published_at, type, ...meta }, ...item }) => ({
      ...item,
      ...meta,
      group: type,
      start_time: moment(first_published_at),
      end_time: moment().add(1, 'year'), // indicates they are live
    }));

  getGroups = items =>
    items
      .map(({ group }) => group)
      .reduce(
        (groups, group, index, arr) =>
          arr.indexOf(group) >= index
            ? groups.concat({
                id: group,
                /* convert 'base.IndexPage' to 'Index Page' */
                title: group.replace(/([a-z](?=[A-Z]))/g, '$1 ').split('.')[1],
              })
            : groups,
        [],
      );

  getDefaultTimes = items =>
    items.reduce(({ start = null, end = null }, { start_time, end_time }) => {
      if (!start && !end) return { start: start_time, end: end_time };
      return {
        start: start_time.isBefore(start) ? start_time : start,
        end: end_time.isAfter(end) ? end_time : end,
      };
    }, {});

  render() {
    const {
      defaultTimes: { start, end },
      error,
      groups,
      isLoading,
      items,
    } = this.state;

    return (
      <div className="timeline">
        {isLoading && <span>Loading...</span>}
        {error && <span>Error: {error.message}</span>}
        {!(isLoading || error) && (
          <Timeline
            defaultTimeStart={start}
            defaultTimeEnd={end}
            groups={groups}
            items={items}
            sidebarWidth={250}
            stackItems={true}
          />
        )}
      </div>
    );
  }
}
