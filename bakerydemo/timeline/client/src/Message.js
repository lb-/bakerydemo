import React from 'react';
import PropTypes from 'prop-types';

/**
 * A verbose example of a Functional component. Message renders the loading or
 * error message states.
 * @param {Object} props
 */
const Message = ({ error, isLoading }) => (
  <div class="messages">
    <ul>
      {isLoading && <li class="success">Loading...</li>}
      {error && <li class="error">Error: {error.message}</li>}
    </ul>
  </div>
);

Message.defaultProps = {
  isLoading: false,
  error: {},
};

Message.propTypes = {
  isLoading: PropTypes.bool,
  error: PropTypes.shape({
    message: PropTypes.string,
  }),
};

export default Message;
