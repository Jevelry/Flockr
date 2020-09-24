import auth
import pytest
from error import InputError

# AUTH_LOGIN tests
# SUCCESSFUL
def test_successful_auth_login():
    user = auth.auth_register('snow@white.com', 'dwarves', 'Snow', 'White')
    auth.auth_logout(user['token'])
    user = auth.auth_login('snow@white.com', 'dwarves')
    assert user['u_id'] == 1
    assert user['token'] == 'snow@white.com'

    user = auth.auth_register('George.Humohrey@bigpond.edu.au', 'washington', 'George', 'Humohrey')
    auth.auth_logout(user['token'])
    user = auth.auth_login('George.Humohrey@bigpond.edu.au', 'washington')
    assert user['u_id'] == 2
    assert user['token'] == 'George.Humohrey@bigpond.edu.au'

    user = auth.auth_register('Artur.Hawking@bing.edu.au', 'manetherin', 'Artur', 'Hawking')
    auth.auth_logout(user['token'])
    user = auth.auth_login('Artur.Hawking@bing.edu.au', 'manetherin')
    assert user['u_id'] == 3
    assert user['token'] == 'Artur.Hawking@bing.edu.au'

# UNSUCCESSFUL

def test_non_existant_email_auth_login():
    user = auth.auth_register('tom-ellis@duckduckgoose.com', 'project', 'Tom', 'Ellis')
    auth.auth_logout(user['token'])
    with pytest.raises(InputError) as e:
        assert auth.auth_login('fake.email@duckduckgoose.com', 'project')

    user = auth.auth_register('DavidWhitecross@gmail.com', 'totenham', 'Ronen', 'Bhaumik')
    auth.auth_logout(user['token'])
    with pytest.raises(InputError) as e:
        assert auth.auth_login('Ronen@gmail.com', 'totenham')

    user = auth.auth_register('Gag..Halfrunt@hhgttg.com', 'justzisguy', 'Gag', 'Halfrunt')
    auth.auth_logout(user['token'])
    with pytest.raises(InputError) as e:
        assert auth.auth_login('Gag.Halfrunt@hhgttg.com', 'justzisguy')

def test_incorrect_password_auth_login():
    user = auth.auth_register('Jeltz@vogon.com', 'hyperspaceplanningcouncil', 'Prostetnic', 'Jeltz')
    auth.auth_logout(user['token'])
    with pytest.raises(InputError) as e:
        assert auth.auth_login('Jeltz@vogon.com', 'regrettably')

    user = auth.auth_register('LewsTherin@dragon.com.au', 'ilenya', 'Lews', 'Therin')
    auth.auth_logout(user['token'])
    with pytest.raises(InputError) as e:
        assert auth.auth_login('LewsTherin@dragon.com.au', 'aviendha')

    user = auth.auth_register('Trent-Zimmerman@council.com.nz', 'election', 'Trent', 'Zimmerman')
    auth.auth_logout(user['token'])
    with pytest.raises(InputError) as e:
        assert auth.auth_login('Trent-Zimmerman@council.com.nz', 'lotsofmail')

# AUTH_REGISTER tests
# Successful
def test_successful_auth_register():
    user = auth.auth_register('elliot@balgara.com', 'spooky', 'Elliot', 'Rotenstein')
    assert user['u_id'] == 1
    assert user['token'] == 'elliot@balgara.com'

    user = auth.auth_register('apple@gmail.com', 'APPLES', 'A', 'Fruit')
    assert user['u_id'] == 2
    assert user['token'] == 'apple@gmail.com'

    user = auth.auth_register('pear@yahoo.com', 'prickly', 'Pear', 'Vegetable')
    assert user['u_id'] == 3
    assert user['token'] == 'pear@yahoo.com'

def test_same_names_auth_register():
    user = auth.auth_register('ben@gmail.com', 'thisisben', 'Ben', 'Batson')
    assert user['u_id'] == 4
    assert user['token'] == 'ben@gmail.com'

    user = auth.auth_register('ben1@gmail.com', 'thisisalsoben', 'Ben', 'Batson')
    assert user['u_id'] == 5
    assert user['token'] == 'ben1@gmail.com'

    user = auth.auth_register('ben2@gmail.com', 'thistooisben', 'Ben', 'Batson')
    assert user['u_id'] == 6
    assert user['token'] == 'ben2@gmail.com'

    user = auth.auth_register('ben3@gmail.com', 'ThirdBenIsACharm', 'Ben', 'Batson')
    assert user['u_id'] == 7
    assert user['token'] == 'ben3@gmail.com'

    user = auth.auth_register('ben4@gmail.com', 'ForAllBenKind', 'Ben', 'Batson')
    assert user['u_id'] == 8
    assert user['token'] == 'ben4@gmail.com'

    user = auth.auth_register('bentennyson@gmail.com', 'BenTen', 'Ben', 'Batson')
    assert user['u_id'] == 9
    assert user['token'] == 'bentennyson@gmail.com'

def test_same_passwords_auth_register():
    user = auth.auth_register('hacker@gmail.com', 'password', 'Alfred', 'Hural')
    assert user['u_id'] == 10
    assert user['token'] == 'hacker@gmail.com'

    user = auth.auth_register('albert@gmail.com', 'password', 'Albert', 'Einsten')
    assert user['u_id'] == 11
    assert user['token'] == 'albert@gmail.com'

    user = auth.auth_register('zaphod@gmail.com', 'password', 'Zaphod', 'Beeblebrox')
    assert user['u_id'] == 12
    assert user['token'] == 'zaphod@gmail.com'

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
    auth.auth_register('alex@gmail.com', 'Ahoy there', 'Alex', 'Hurkins')
    with pytest.raises(InputError) as e:
        assert auth.auth_register('alex@gmail.com', 'Thisissosad', 'Alex', 'Robbie')
    
    auth.auth_register('james@hotmail.com.au', 'GiantPeach', 'James', 'Manetherin')
    with pytest.raises(InputError) as e:
        assert auth.auth_register('james@gmail.com', 'Jupiter', 'James', 'Planetarium')
        assert auth.auth_register('james@gmail.com', 'enter password', 'James', 'Jameson')

    auth.auth_register('captain@gmail.com', 'yoghurt', 'Hubert', 'Love')
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

    with pytest.raises(InputError) as e:
        assert auth.auth_register('first@name.com', 'antihippopotomonstrosesquippedaliophobia', 'Jay', '')