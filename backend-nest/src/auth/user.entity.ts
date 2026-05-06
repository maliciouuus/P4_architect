import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

/**
 * Entité TypeORM représentant un utilisateur en base de données.
 *
 * Une entité est la correspondance directe entre une classe TypeScript et une table SQL.
 * TypeORM se charge de créer la table et de mapper les colonnes automatiquement.
 *
 * Table cible : accounts_user_nest (nom explicite pour ne pas écraser d'autres tables)
 */
@Entity('accounts_user_nest')
export class User {
  // Clé primaire auto-incrémentée — TypeORM génère le SERIAL/BIGSERIAL PostgreSQL
  @PrimaryGeneratedColumn()
  id: number;

  // Email unique : contrainte d'unicité gérée par PostgreSQL (index UNIQUE)
  @Column({ unique: true })
  email: string;

  // Nom d'affichage de l'utilisateur — pas nécessairement unique
  @Column()
  username: string;

  // Mot de passe hashé avec bcrypt — jamais stocké en clair
  @Column()
  password: string;

  // Date de création remplie automatiquement par TypeORM à l'insertion
  @CreateDateColumn()
  createdAt: Date;
}
