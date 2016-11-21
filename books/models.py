# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Test(models.Model):
    cash = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Test'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Authors(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'authors'


class Books(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    pub = models.ForeignKey('Publishers', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class BooksBook(models.Model):
    book_title = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'books_book'


class BooksDiscussion(models.Model):
    username = models.CharField(max_length=30)
    message = models.CharField(max_length=500)
    book = models.ForeignKey(BooksBook, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_discussion'


class Checkouts(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    returned_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checkouts'


class Discusses(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)
    post_time = models.DateTimeField()
    post_text = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'discusses'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Follows(models.Model):
    author = models.ForeignKey(Authors, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'follows'


class Notifications(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='user', blank=True, null=True)
    body = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class Publishers(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'publishers'


class Users(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'users'


class Wrote(models.Model):
    author = models.ForeignKey(Authors, models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wrote'
