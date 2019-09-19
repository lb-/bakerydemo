/* eslint-disable camelcase */
import moment from 'moment';

const getTransformedItems = ({ items = [] } = {}) =>
  items.map(({ meta: { first_published_at, type, ...meta }, ...item }) => ({
    ...item,
    ...meta,
    group: type,
    start_time: moment(first_published_at),
    end_time: moment().add(1, 'year'), // indicates they are live
  }));

const getGroups = items =>
  items
    .map(({ group }) => group)
    .reduce((groups, group, index, arr) => {
      if (arr.indexOf(group) >= index) {
        return groups.concat({
          id: group,
          /* convert 'base.IndexPage' to 'Index Page' */
          title: group.replace(/([a-z](?=[A-Z]))/g, '$1 ').split('.')[1],
        });
      }
      return groups;
    }, []);

const getDefaultTimes = items =>
  items.reduce(({ start = null, end = null }, { start_time, end_time }) => {
    if (!start && !end) return { start: start_time, end: end_time };
    return {
      start: start_time.isBefore(start) ? start_time : start,
      end: end_time.isAfter(end) ? end_time : end,
    };
  }, {});

const transformer = response => {
  const items = getTransformedItems(response);
  return {
    defaultTimes: getDefaultTimes(items),
    groups: getGroups(items),
    items,
  };
};

export default transformer;
