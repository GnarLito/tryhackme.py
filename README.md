<p><img src="https://assets.tryhackme.com/img/THMlogo.png" width="350" title="TryHackMe Logo"></p>


 
Maintained Python wrapper for TryHackMe public API  
This fork is unofficial and not associated with TryHackMe, but i would love to.

## Installation
```sh
pip3 install tryhackme.py
```

## Example
```python
import tryhackme

client = tryhackme.Client(session="<tryHackMe cookie: `connect.sid`>") # Logging in is optional
client.get_stats() # {'publicRooms': 203, 'totalUsers': 88017, 'cloneableRooms': 967}

```
For more info over getting the `connect.sid` visit [#1][i1]

## API documentation
For the API documentation please visit the [TryHackMe-API-Doc](https://github.com/GnarLito/TryHackMe-API-Doc)


## Contributing
You're welcome to create Issues/Pull Requests with features you'd want to see

## License
[MIT LICENSE](https://github.com/szymex73/py-thmapi/blob/master/LICENSE)

[i1]: https://github.com/GnarLito/tryhackme.py/issues/1
