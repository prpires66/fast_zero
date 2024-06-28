from sqlalchemy import select

from fast_zero.models import User


def test_cSreate_user(session):
    user = User(
        username='dunossauro', email='email@email.com', password='secret'
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'email@email.com')
    )

    assert result.id == 1
