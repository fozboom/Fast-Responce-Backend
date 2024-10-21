## Проблемы с ENUM

Допустим, у нас есть такая колонка:

```python
sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='genderenum'), nullable=False)
```

При первом запуске миграции Alembic корректно создаст таблицу и ENUM-тип для этой колонки. 
Однако если в будущем вы захотите изменить этот ENUM (например, добавить новое значение), 
при повторных миграциях вы можете столкнуться с ошибкой, так как Alembic попытается создать тип genderenum, 
который уже существует в базе данных.

### Решение
Чтобы избежать этой проблемы, нужно явно указать параметр create_type=False, 
чтобы Alembic не пытался повторно создать ENUM-тип:


```python
sa.Column('gender', sa.Enum('MALE', 'FEMALE', name='genderenum', create_type=False), nullable=False)
```

## Проблемы при откате миграций (downgrade)
При удалении таблиц с помощью Alembic таблицы удаляются, но связанные с ними ENUM-ы остаются в базе данных. 
Это может привести к конфликтам, если в будущем вы захотите использовать те же имена для новых ENUM-типов.

### Решение
Чтобы Alembic корректно удалял типы ENUM при откате миграций, нужно расширить метод downgrade следующим образом:
    
```python
def downgrade() -> None:
    # Удаление таблиц
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_table('profiles')
    
    # Удаление типов ENUM
    op.execute('DROP TYPE IF EXISTS ratingenum')
    op.execute('DROP TYPE IF EXISTS genderenum')
    op.execute('DROP TYPE IF EXISTS professionenum')
    op.execute('DROP TYPE IF EXISTS statuspost')
```

В этом случае, при откате миграции, будут удалены не только таблицы, но и все соответствующие ENUM-типов.

Важно: Используйте этот метод только тогда, когда необходимо удалить сами ENUM-типы, чтобы не допустить ненужного удаления, если типы могут понадобиться в других частях приложения.

