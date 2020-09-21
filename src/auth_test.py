import auth
import pytest
from error import InputError

# AUTH_REGISTER tests
# Successful
def test_successful_auth_register():
    user = auth.auth_register('elliot@balgara.com', 'spooky', 'Elliot', 'Rotenstein')
    assert user['u_id'] == 1
    assert user['token'] == 'ElliotRotenstein'

    user = auth.auth_register('apple@gmail.com', 'APPLES', 'A', 'Fruit')
    assert user['u_id'] == 2
    assert user['token'] == 'AFruit'

    user = auth.auth_register('pear@yahoo.com', 'prickly', 'Pear', 'Vegetable')
    assert user['u_id'] == 3
    assert user['token'] == 'PearVegetable'

def test_same_names_auth_register():
    user = auth.auth_register('ben@gmail.com', 'thisisben', 'Ben', 'Batson')
    assert user['u_id'] == 4
    assert user['token'] == 'BenBatson'

    user = auth.auth_register('ben1@gmail.com', 'thisisalsoben', 'Ben', 'Batson')
    assert user['u_id'] == 5
    assert user['token'] == 'BenBatson1'

    user = auth.auth_register('ben2@gmail.com', 'thistooisben', 'Ben', 'Batson')
    assert user['u_id'] == 6
    assert user['token'] == 'BenBatson2'

    user = auth.auth_register('ben3@gmail.com', 'ThirdBenIsACharm', 'Ben', 'Batson')
    assert user['u_id'] == 7
    assert user['token'] == 'BenBatson3'

    user = auth.auth_register('ben4@gmail.com', 'ForAllBenKind', 'Ben', 'Batson')
    assert user['u_id'] == 8
    assert user['token'] == 'BenBatson4'

    user = auth.auth_register('bentennyson@gmail.com', 'BenTen', 'Ben', 'Batson')
    assert user['u_id'] == 9
    assert user['token'] == 'BenBatson5'

def test_same_passwords_auth_register():
    user = auth.auth_register('hacker@gmail.com', 'password', 'Alfred', 'Hural')
    assert user['u_id'] == 10
    assert user['token'] == 'AlfredHural'

    user = auth.auth_register('albert@gmail.com', 'password', 'Albert', 'Einsten')
    assert user['u_id'] == 11
    assert user['token'] == 'AlbertEinstein'

    user = auth.auth_register('zaphod@gmail.com', 'password', 'Zaphod', 'Beeblebrox')
    assert user['u_id'] == 12
    assert user['token'] == 'ZaphodBeeblebrox'

# Unsuccessful

def test_invalid_email_auth_register():
    with pytest.raises(InputError) as e:
        assert auth.auth_register('email', 'Mark@gmail.com', 'Mark', 'Klup')
    
    with pytest.raises(InputError) as e:
        assert auth.auth_register('Fred@gmail', '123456789', 'Fred', 'Tolmer')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('@gmail.com', 'Adams email', 'Aaron', 'Cravve')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('john@doe.', 'Abpruptly', 'John', 'Doe')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('Nic123Atgmail.com', 'ThisIsASpanishName?', 'Nicolas', 'Santiago')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('Bob@the@builder.com', 'Can we do it?', 'Bob', 'theBuilder')


def test_existing_email_auth_register():
    user = auth.auth_register('alex@gmail.com', 'Ahoy there', 'Alex', 'Hurkins')
    with pytest.raises(InputError) as e:
        assert auth.auth_register('alex@gmail.com', 'Thisissosad', 'Alex', 'Robbie')
    
    user = auth.auth_register('james@hotmail.com.au', 'GiantPeach', 'James', 'Manetherin')
    with pytest.raises(InputError) as e:
        assert auth.auth_register('james@gmail.com', 'Jupiter', 'James', 'Planetarium')
        assert auth.auth_register('james@gmail.com', 'enter password', 'James', 'Jameson')

    user = auth.auth_register('captain@gmail.com', 'yoghurt', 'Hubert', 'Love')
    with pytest.raises(InputError) as e:
        assert auth.auth_register('captain@gmail.com', 'captain', 'Arthur', 'Wolban')

def test_invalid_password_auth_register():
    with pytest.raises(InputError) as e:
        assert auth.auth_register('yellow@gmail.com', '', 'Yellow', 'Submarine')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('arjun602@gmail.com', '12345', 'Arjun', 'Mukherjee')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('arid@desert.com', 'five', 'Monroe', 'Smith')


def test_invalid_first_name_auth_register():
    with pytest.raises(InputError) as e:
        assert auth.auth_register('long@name.com', 'huuuuge', 'thisisareallylongnameanditjustkeepsgoingandgoingwhenwillitend', 'Stevens')

    with pytest.raises(InputError) as e:
        assert auth.auth_register('no@name.com', 'Hello, World!', '', 'Tapher')

def test_invalid_last_name_auth_register():
    with pytest.raises(InputError) as e:
        assert auth.auth_register('ripley@optus.com', 'This is the end.', 'Hugh', 'Imsickoftestingthisfunctionsoitsagoodthingitsdone!')
