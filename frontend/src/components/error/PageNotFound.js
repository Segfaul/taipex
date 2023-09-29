import React, { useEffect } from 'react';

const PageNotFound = () => {
  useEffect(() => {
    document.title = 'Страница не найдена | Taipex';
  }, []);

  return (
    <div className='error'>
      <h1>Ошибка 404: Страница не найдена</h1>
      <p>К сожалению, запрошенная вами страница не существует или находится в разработке.</p>
    </div>
  );
};

export default PageNotFound;